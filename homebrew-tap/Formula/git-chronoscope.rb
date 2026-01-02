# git-chronoscope Homebrew Formula for Tap Repository
# This file is also available in Formula/git-chronoscope.rb

class GitChronoscope < Formula
  include Language::Python::Virtualenv

  desc "Generate time-lapse visualizations of Git repository evolution"
  homepage "https://github.com/user/git-chronoscope"
  url "https://github.com/user/git-chronoscope/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256_WILL_BE_UPDATED_ON_RELEASE"
  license "MIT"
  head "https://github.com/user/git-chronoscope.git", branch: "main"

  depends_on "python@3.11"
  depends_on "ffmpeg"
  depends_on "git"

  resource "GitPython" do
    url "https://files.pythonhosted.org/packages/source/G/GitPython/GitPython-3.1.40.tar.gz"
    sha256 "22b126e9ffb671fdd0c129796343a02f069a7e8a5abb0eb0c71d1a1b5d14db3c"
  end

  resource "Pillow" do
    url "https://files.pythonhosted.org/packages/source/P/Pillow/Pillow-10.1.0.tar.gz"
    sha256 "e6bf8de6c36ed96c86ea3b6e1d5273c53f46ef518a062464cd7ef5dd2cf92e38"
  end

  resource "Pygments" do
    url "https://files.pythonhosted.org/packages/source/P/Pygments/Pygments-2.17.2.tar.gz"
    sha256 "da46cec9fd2de5be3a8a784f434e4c4ab670b4ff54d605c4c2717e9d49c4c367"
  end

  resource "tqdm" do
    url "https://files.pythonhosted.org/packages/source/t/tqdm/tqdm-4.66.1.tar.gz"
    sha256 "d88e651f9db8d8551a62556d3cff9e3034274ca5d66e93197cf2490e2dcb69c7"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"git-chronoscope", "--help"
  end
end
